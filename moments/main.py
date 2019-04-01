import numpy as np
import matplotlib.pyplot as plt

from moments.models import NBDAnalyticRetreiver, BinMoment
from moments.utils import draw_and_save


def main():
    readers = [
        NBDAnalyticRetreiver('norm1', 'Nbd ; counts'),
        # GaussLikeRetreiver('norm1', 'Random Nev=1e8; x; counts', (1, 60))
    ]
    n, p = 70, 0.5
    hists = [r.eval(95, (30, 125), start=30, stop=125,
                    n=n, p=p, gamma=1., sigma=1., ssize=100)
             for r in readers]

    colors = [38, 46]

    for h, c in zip(hists, colors):
        binner = BinMoment(h)
        coef = binner.moments()
        # print 'coefs', coef
        j = np.arange(coef.size) + 1
        # plt.plot(j, coef , label = h.GetTitle())
        plt.plot(j[0:60], coef[0:60], 'o-', label=h.GetTitle() +
                 ' n =  %d, p = %.2g' % (n, p))
        plt.legend(loc='lower center')
        plt.xlabel('j -- bin number')
        plt.ylabel('C_{j}')
        # plt.yscale('log')
        h.SetLineColor(c)
        h.Scale(1. / h.Integral())
        h.Draw('hist same')

    name = hists[0].GetName()
    draw_and_save('jhist_' + name, True, True)
    plt.savefig('jc_' + name + '.png')
    plt.show()


if __name__ == '__main__':
    main()
