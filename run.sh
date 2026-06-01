#!/bin/bash
if [ ! -d "data/input" ]; then
  echo "ERROR: data/input directory not found"
  exit 1
fi

echo "Starting mail processor..."
python3 -m app.main
echo "Done."
