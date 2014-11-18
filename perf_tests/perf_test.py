import time
import subprocess

class PerfTest(object):
    """Class for performance testing"""

    # Quantiles of Student distribution for 95% probability
    quantile = {}
    quantile[2] = 4.3027
    quantile[3] = 3.1824
    quantile[4] = 2.7764
    quantile[5] = 2.5706
    quantile[10] = 2.2281
    quantile[15] = 2.1314
    quantile[20] = 2.0860
    quantile[25] = 2.0595
    quantile[50] = 2.0086
    quantile[100] = 1.9840
    quantile[1000] = 1.9623
    quantile_inf = 1.96

    @classmethod
    def get_quantile(cls, n_runs):
        """Returns quantile of Student distribution"""
        max_n_runs = max(cls.quantile.keys())

        if not n_runs in cls.quantile and n_runs <= max_n_runs:
            raise ValueError("No quantile value for given n_runs, see perf_test.py for list of quantiles")

        if n_runs > max_n_runs:
            return cls.quantile[max_n_runs]
        return cls.quantile[n_runs]

    @classmethod
    def test_performance(cls, cmd, n_runs=3):
        """Tests performance of some function, makes n_runs+1 runs to avoid strange quantiles"""
        if n_runs <= 0:
            raise ValueError("Bad argument n_runs: must be positive")
        if type(cmd) is not str:
            raise ValueError("Cmd must be a string")

        # warm up
        subprocess.call(['python', '-c', cmd])

        n_runs += 1
        times = [0] * (n_runs)
        for i in xrange(n_runs):
            start = time.time()
            subprocess.call(['python', '-c', cmd])
            times[i] = time.time() - start

        mean = sum(times) / n_runs
        dev = sum([(t - mean)**2 for t in times]) / (n_runs - 1)
        interval = ((dev / n_runs) ** 0.5) * cls.get_quantile(n_runs - 1)

        print("%s: %f+-%f" % (cmd, mean, interval))
