#!/bin/bash

NAME=$1
ROOT="static/problemset/$NAME"

TEX_FILE="$ROOT/$NAME.tex"
PDF_FILE="$ROOT/$NAME.pdf"
SVG_FILE="$ROOT/$NAME.svg"

TEX_FILE_SOLUTION="$ROOT/$NAME-solution.tex"
PDF_FILE_SOLUTION="$ROOT/$NAME-solution.pdf"
SVG_FILE_SOLUTION="$ROOT/$NAME-solution.svg"

if [ -f "$TEX_FILE" ]; then
  pdflatex -interaction=nonstopmode -output-directory="$ROOT" $TEX_FILE
  pdf2svg $PDF_FILE $SVG_FILE

  # same for file with solution
  pdflatex -interaction=nonstopmode -output-directory="$ROOT" $TEX_FILE_SOLUTION
  pdf2svg $PDF_FILE_SOLUTION $SVG_FILE_SOLUTION
else 
  echo "$TEX_FILE does not exist."
fi
