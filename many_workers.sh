#!/bin/sh

for i in {1..10}
do
    tmux split-window
    tmux select-layout tiled
done

clear

tmux select-layout tiled

tmux setw synchronize-panes on
