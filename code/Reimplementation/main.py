from Controller import Controller

def main():
    configs = [
        {
            "amount_of_frames": 1000,
            # TODO: add more config
        }
    ]

    controller = Controller()
    controller.set_config(configs[0])
    controller.start()

if __name__ == "__main__":
    main()