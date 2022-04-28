import io_helper
import helper

if __name__ == '__main__':
    args = io_helper.parse_args()
    io_helper.init(args)
    if helper.CONSTANTS.DEBUG_MODE:
        io_helper.print_func("debug mode is on")