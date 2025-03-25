#!/bin/bash

# Set up script to exit on error
set -e

# Default values for optional arguments
ENV_NAME="productivity_loss_v2"
DEFAULT_INPUT="data/test_assets.csv"
DEFAULT_LOSS_FUNCTION="HOTHAPS"
DEFAULT_PLOTS="False"
DEFAULT_SCENARIOS="SSP126,SSP245,SSP370,SSP585"
DEFAULT_PROJECT="test"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --input) INPUT_FILE="$2"; shift ;;
        --loss-function) LOSS_FUNCTION="$2"; shift ;;
        --make-plots) DEFAULT_PLOTS="$2"; shift ;;
        --scenarios) SCENARIOS="$2"; shift ;;
        --project) PROJECT="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Use defaults if arguments are not provided
INPUT_FILE="${INPUT_FILE:-$DEFAULT_INPUT}"
LOSS_FUNCTION="${LOSS_FUNCTION:-$DEFAULT_LOSS_FUNCTION}"
MAKE_PLOTS="${MAKE_PLOTS:-$DEFAULT_PLOTS}"
SCENARIOS="${SCENARIOS:-$DEFAULT_SCENARIOS}"
PROJECT="${PROJECT:-$DEFAULT_PROJECT}"

# Run the model with arguments
echo "Running Productivity Loss Model for project $PROJECT with:"
echo "   📂 Input File: $INPUT_FILE"
echo "   💾 Output Files: /output_csvs/"
echo "   🔧 Loss Function: $LOSS_FUNCTION"
echo "   📊 Generate plots?: $MAKE_PLOTS"
echo "   🚀 Scenarios: $SCENARIOS"

python3 src/main.py --input "$INPUT_FILE" --loss-function "$LOSS_FUNCTION" --makeplots "$MAKE_PLOTS" --scenarios "$SCENARIOS" --project "$PROJECT"

# # Notify user of completion
echo "Model run completed! Let's go! Results saved in: /output_csvs"