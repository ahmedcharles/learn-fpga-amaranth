from amaranth_boards.icebreaker import ICEBreakerPlatform

from top import Top

if __name__ == "__main__":
    platform = ICEBreakerPlatform()
    platform.add_resources(platform.break_off_pmod)

    # The platform allows access to the various resources defined by the board
    # definition from amaranth-boards.
    led0 = platform.request('led_r', 1)
    led1 = platform.request('led_g', 1)
    led2 = platform.request('led_g', 2)
    led3 = platform.request('led_g', 3)
    led4 = platform.request('led_g', 4)
    leds = [led0, led1, led2, led3, led4]
    uart = platform.request('uart', 0)

    platform.build(Top(leds, uart), do_program=True)

