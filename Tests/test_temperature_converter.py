import unittest
from subprocess import run

# test if file exists

executable = "temperature_converter"

class TestTemperatureConverter(unittest.TestCase):
    def test_celsius_to_celsius_good_high(self):
        input_data = "Alice\n"
        expected_output = "Hello, Alice!"

        process = run(['python', 'my_script.py'], input=input_data.encode(), capture_output=True, text=True)

        self.assertIn(expected_output, process.stdout)

    def test_celsius_to_celsius_good_medium(self):
        pass

    def test_celsius_to_celsius_good_low(self):
        pass

    def test_celsius_to_celsius_bad(self):
        pass

    def test_celsius_to_fahrenheit_good_high(self):
        pass

    def test_celsius_to_fahrenheit_good_medium(self):
        pass

    def test_celsius_to_fahrenheit_good_low(self):
        pass

    def test_celsius_to_fahrenheit_bad(self):
        pass

    def test_celsius_to_kelvin_good_high(self):
        pass

    def test_celsius_to_kelvin_good_medium(self):
        pass

    def test_celsius_to_kelvin_good_low(self):
        pass

    def test_celsius_to_kelvin_bad(self):
        pass

    def test_fahrenheit_to_celsius_good_high(self):
        pass

    def test_fahrenheit_to_celsius_good_medium(self):
        pass

    def test_fahrenheit_to_celsius_good_low(self):
        pass

    def test_fahrenheit_to_celsius_bad(self):
        pass

    def test_fahrenheit_to_fahrenheit_good_high(self):
        pass

    def test_fahrenheit_to_fahrenheit_good_medium(self):
        pass

    def test_fahrenheit_to_fahrenheit_good_low(self):
        pass

    def test_fahrenheit_to_fahrenheit_bad(self):
        pass

    def test_fahrenheit_to_kelvin_good_high(self):
        pass

    def test_fahrenheit_to_kelvin_good_medium(self):
        pass

    def test_fahrenheit_to_kelvin_good_low(self):
        pass

    def test_fahrenheit_to_kelvin_bad(self):
        pass

    def test_kelvin_to_celsius_good_high(self):
        pass

    def test_kelvin_to_celsius_good_medium(self):
        pass

    def test_kelvin_to_celsius_good_low(self):
        pass

    def test_kelvin_to_celsius_bad(self):
        pass

    def test_kelvin_to_fahrenheit_good_high(self):
        pass

    def test_kelvin_to_fahrenheit_good_medium(self):
        pass

    def test_kelvin_to_fahrenheit_good_low(self):
        pass

    def test_kelvin_to_fahrenheit_bad(self):
        pass

    def test_kelvin_to_kelvin_good_high(self):
        pass

    def test_kelvin_to_kelvin_good_medium(self):
        pass

    def test_kelvin_to_kelvin_good_low(self):
        pass

    def test_kelvin_to_kelvin_bad(self):
        pass


if __name__ == "__main__":
    unittest.main()
