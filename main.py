# main.py
from argument import parse_args, save_thresholds
from logic import collect_args_and_print
from daemon import run_daemon_mode

def main():
    """
    Entry point of the System Monitor program.
    """
    args = parse_args()

    # Save thresholds (to config.json)
    save_thresholds(args.warning, args.danger)

    if args.daemon:
        run_daemon_mode(args, args.warning, args.danger, args.interval)
    else:
        collect_args_and_print(args, args.warning, args.danger)


if __name__ == "__main__":
    main()
