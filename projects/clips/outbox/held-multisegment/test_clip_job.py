#!/usr/bin/env python3
"""Tests for clip_job cut_ranges / ranges / lint (single-range path and multi-segment path).
Run: python3 -I pipeline/tests/test_clip_job.py   (builds a 30 s synthetic source: 3 s colour blocks + a tone)"""
import os, re, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import clip_job  # noqa: E402

FF = clip_job.FFMPEG


def dur(p):
    return clip_job.ffinfo(p)["duration"]


def mean_colour(p, t):
    """Average RGB of the frame at t seconds."""
    out = subprocess.run([FF, "-loglevel", "error", "-ss", str(t), "-i", p, "-frames:v", "1", "-vf", "scale=1:1",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return tuple(out[:3])


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp()
        cls.src = os.path.join(cls.d, "src.mp4")
        # ten 3 s blocks: red, green, blue, red, green, blue, ... so a segment's colour identifies its source position
        cols = ["red", "green", "blue"]
        inputs, fl = [], []
        for i in range(10):
            inputs += ["-f", "lavfi", "-i", f"color=c={cols[i % 3]}:s=320x180:r=30:d=3"]
        concat = "".join(f"[{i}:v]" for i in range(10)) + "concat=n=10:v=1:a=0[v]"
        subprocess.run([FF, "-y", "-loglevel", "error", *inputs, "-f", "lavfi", "-i", "sine=f=440:d=30",
                        "-filter_complex", concat, "-map", "[v]", "-map", "10:a", "-c:v", "libx264", "-c:a", "aac",
                        "-shortest", cls.src], check=True)

    def test_ranges(self):
        self.assertEqual(clip_job.ranges({"start": 1, "end": 4}), [(1.0, 4.0)])
        self.assertEqual(clip_job.ranges({"start": 1, "end": 4, "segments": [[5, 7], [1, 2]]}), [(5.0, 7.0), (1.0, 2.0)])
        self.assertAlmostEqual(clip_job.total_length({"segments": [[5, 7], [1, 2.5]]}), 3.5)

    def test_single_range(self):
        out = os.path.join(self.d, "single.mp4")
        clip_job.cut_ranges(self.src, [(3.2, 9.2)], out)
        self.assertAlmostEqual(dur(out), 6.0, delta=0.15)
        r, g, b = mean_colour(out, 1.0)  # source 4.2 s = block 1 = green
        self.assertTrue(g > r and g > b)
        self.assertFalse(os.path.exists(os.path.join(self.d, "single.part0.mp4")))

    def test_multi_segment_order_and_length(self):
        out = os.path.join(self.d, "multi.mp4")
        # blue block (6.5-8.5 -> blue? 6.5 s = block 2 = blue), then red (0.5-2.5), then green (3.5-5.5)
        clip_job.cut_ranges(self.src, [(6.5, 8.5), (0.5, 2.5), (3.5, 5.5)], out)
        self.assertAlmostEqual(dur(out), 6.0, delta=0.3)
        r, g, b = mean_colour(out, 1.0)
        self.assertTrue(b > r and b > g, "first part should be the blue range")
        r, g, b = mean_colour(out, 3.0)
        self.assertTrue(r > g and r > b, "second part should be the red range")
        r, g, b = mean_colour(out, 5.0)
        self.assertTrue(g > r and g > b, "third part should be the green range")
        self.assertTrue(clip_job.ffinfo(out)["audio"])
        self.assertEqual([f for f in os.listdir(self.d) if ".part" in f], [])

    def _spec(self, **kw):
        s = {"id": "t", "campaign": "mrbeast-gaming-mw4", "source": self.src, "hook": "Three plain test words here",
             "caption": "c", "required_tags": ["#MW4"], "tiktok_caption": "x #MW4", "instagram_caption": "y #MW4",
             "schedule": {}, "footage": "campaign-supplied"}
        s.update(kw)
        return s

    def test_lint_lengths(self):
        self.assertEqual(clip_job.lint(self._spec(start=0, end=20), False), [])
        self.assertEqual(clip_job.lint(self._spec(segments=[[0, 8], [10, 20]]), False), [])
        self.assertTrue(any("outside 15-59" in e for e in clip_job.lint(self._spec(segments=[[0, 4], [6, 9]]), False)))
        self.assertTrue(any("at least 2" in e for e in clip_job.lint(self._spec(segments=[[0, 20]]), False)))
        self.assertTrue(any("start" in e for e in clip_job.lint(self._spec(), False)))
        self.assertTrue(any("reversed" in e for e in clip_job.lint(self._spec(segments=[[9, 3], [10, 30]]), False)))


if __name__ == "__main__":
    unittest.main()
