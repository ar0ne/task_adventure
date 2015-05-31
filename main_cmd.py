from tasks import TaskController



if __name__ == '__main__':
    controller = TaskController.load()
    if controller is None:
        controller = TaskController()

    controller.run()

