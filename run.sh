#!/bin/bash

# Set up script to exit on error
set -e

# Default values for optional arguments
ENV_NAME="productivity_loss_v2"
DEFAULT_INPUT="data/test_assets.csv"
DEFAULT_OUTPUT="data/test_outputs.csv"
DEFAULT_LOSS_FUNCTION="HOTHAPS"
DEFAULT_PLOTS="FALSE"
# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --input) INPUT_FILE="$2"; shift ;;
        --output) OUTPUT_FILE="$2"; shift ;;
        --loss-function) LOSS_FUNCTION="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Use defaults if arguments are not provided
INPUT_FILE="${INPUT_FILE:-$DEFAULT_INPUT}"
OUTPUT_FILE="${OUTPUT_FILE:-$DEFAULT_OUTPUT}"
LOSS_FUNCTION="${LOSS_FUNCTION:-$DEFAULT_LOSS_FUNCTION}"
MAKE_PLOTS="${MAKE_PLOTS:-$DEFAULT_PLOTS}"

# Run the model with arguments
echo "Running Productivity Loss Model with:"
echo "   📂 Input File: $INPUT_FILE"
echo "   💾 Output File: $OUTPUT_FILE"
echo "   🔧 Loss Function: $LOSS_FUNCTION"
echo "   🔧 Generate plots?: $MAKE_PLOTS"

# python src/main.py --input "$INPUT_FILE" --output "$OUTPUT_FILE" --loss-function "$LOSS_FUNCTION" --makeplots "$MAKE_PLOTS"

# # Notify user of completion
# echo "Model run completed! Let's go! Results saved in: $OUTPUT_FILE"