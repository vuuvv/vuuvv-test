import vuuvv.tasks

@task()
def runserver(t):
	m = __import__("app")
	m.run()
