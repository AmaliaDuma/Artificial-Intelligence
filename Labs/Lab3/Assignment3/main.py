import controller, repository, ui
import time
def main():

    repo = repository.Repository()
    cont = controller.Controller(repo)
    view = ui.UI(cont, repo)

    view.run_menu()

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()