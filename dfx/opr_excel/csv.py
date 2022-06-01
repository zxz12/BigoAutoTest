import os.path

import pandas as pd
from dfx.CONSTANT import CONSTANT


def write_csv(header, datas):
    path = os.path.join(CONSTANT.RES_PATH, 'debt_asset_ratio.csv')
    pd_f = pd.DataFrame(datas)
    f = pd_f.to_csv(path, header=header, index=False,encoding='utf-8')
    return f
