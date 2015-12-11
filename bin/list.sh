#!/usr/bin/env bash
folder=$(dirname $(realpath $0))
for groups in DS Slither Col Hanoi IS Knight Laby Magic Maze NL Pack Sol Soko ; do
    $folder/potassco_csv_max $1 $groups # | $folder/csvcolorlook;
done;
