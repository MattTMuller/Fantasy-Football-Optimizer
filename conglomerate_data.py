positions = ('DB','DL','DST','K','LB','QB','RB','TE','WR')

import os
import pandas as pd

src_dir = "raw_data"
target_dir = "data"

for position in positions:
    players = os.listdir(f"{src_dir}/{position}")
    player_dfs = (pd.read_csv(f'{src_dir}/{position}/{player}') for player in players)
    position_df = pd.concat(player_dfs,ignore_index=True)
    position_df.to_csv(f'data/{position}.csv',index=False)

