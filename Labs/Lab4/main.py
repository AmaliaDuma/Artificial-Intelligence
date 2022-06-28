import controller
import repository
import ui


def main():
    repo = repository.Repository()
    cont = controller.Controller(repo)
    view = ui.UI(cont, repo)

    view.run_menu()


if __name__ == "__main__":
    # call the main function
    main()
