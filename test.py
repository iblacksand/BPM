import click

# Testing printing out the data
def start():
    click.clear()
    with click.progressbar(range(0, 10)) as bar:
        for x in bar:
            click.echo("\nCurrent BPM: " + str(60 + x) + "\n" + "Average BPM: "+ str(120 + x))
            click.confirm("", abort=True)
            click.clear()

if __name__ == '__main__':
    start()