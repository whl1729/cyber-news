#!/bin/bash
OUT_DIR="/home/along/backup/mongodb"
cp -r "${OUT_DIR}" "${OUT_DIR}.old"
mongodump --host localhost --port 27017 --out "${OUT_DIR}" |& tee "${OUT_DIR}/output.log"
