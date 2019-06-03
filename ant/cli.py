"""
cli
***

:Author: tobijjah
:Date: 03.06.19
"""
import click

from ant.controller import Controller


# TODO alter settings

@click.command()
@click.option('-s', '--screen', 'screen_size', default=(900, 900), nargs=2, type=int,
              help='Size of the display, please enter width and height.')
@click.option('-f', '--field', 'field_size', default=(30, 30), nargs=2, type=int,
              help='Size of the game field, please enter rows and columns.')
@click.option('-nh', '--neighbours', 'neighbours', default=4, type=int,
              help='Number of neighbours, please select 4 or 8.')
@click.option('-t', '--torus', 'torus', default=False, type=bool,
              help='Should be the game field a torus, please select true of false.')
@click.option('-ns', '--nutrients', 'nutrients', default=1000, type=int,
              help='How many nutrient units to spawn per site.')
@click.option('-at', '--ant_type', 'ant_type', default='simple', type=str,
              help='The ant type, please select simple or smart.')
def main(screen_size, field_size, neighbours, torus, nutrients, ant_type):
    controller = Controller(screen_size, field_size, neighbours, torus, nutrients, ant_type)
    controller.run()


if __name__ == '__main__':
    main()
