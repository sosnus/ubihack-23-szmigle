### Alg
1. read adc (2x light, knob)
2. map ADC to 0-100
3. chceck if adc_light_control < adc_knob
    * true: pwmRedLed +1
    * false: pwmRedLed -1