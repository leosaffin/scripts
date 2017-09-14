from scripts.papers import plotdir

plotdir = plotdir + 'project/tropopause/'


def add_labels_6_panel(fig):
    # Add letters to 6-panel figure
    fig.text(0.125, 0.92, '(a)')
    fig.text(0.4, 0.92, '(b)')
    fig.text(0.675, 0.92, '(c)')
    fig.text(0.125, 0.48, '(d)')
    fig.text(0.4, 0.48, '(e)')
    fig.text(0.675, 0.48, '(f)')

    return


def add_labels_4_panel(fig):
    # Add letters to 4-panel figure
    fig.text(0.125, 0.91, '(a)')
    fig.text(0.55, 0.91, '(b)')
    fig.text(0.125, 0.56, '(c)')
    fig.text(0.55, 0.56, '(d)')
