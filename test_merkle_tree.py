import subprocess
from glob import glob


def assert_output(input_data, expected_stdout):
    res = subprocess.run(['python', 'ex1.py'], input='\n'.join(input_data).encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert not res.stderr, res.stderr.decode()
    assert res.returncode == 0

    lines = res.stdout.decode().splitlines()
    for i, (outline, expected_line) in enumerate(zip(lines, expected_stdout)):
        assert outline == expected_line, f'wrong input line {i}, expected:\n{expected_line!r}\nbut got:\n{outline}'
    assert len(lines) == len(expected_stdout)


def test_outputs():
    for fname in glob('testcases/case*.txt'):
        print(f'checking {fname}..')
        with open(fname) as fp:
            lines = [l.rstrip() for l in fp]
            inputs = lines[::2]
            outputs = lines[1::2]

        assert_output(inputs, outputs)


if __name__ == '__main__':
    test_outputs()
