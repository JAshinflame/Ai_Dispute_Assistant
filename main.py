#!/usr/bin/env python3
import argparse
import os
from .pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser(description='AI-Powered Dispute Assistant - run pipeline')
    parser.add_argument('--disputes', required=True, help='Path to disputes CSV')
    parser.add_argument('--transactions', required=True, help='Path to transactions CSV')
    parser.add_argument('--out_classified', default='/mnt/data/classified_disputes.csv', help='Output path for classified_disputes.csv')
    parser.add_argument('--out_resolutions', default='/mnt/data/resolutions.csv', help='Output path for resolutions.csv')
    args = parser.parse_args()

    if not os.path.exists(args.disputes):
        print(f'Error: disputes file not found: {args.disputes}')
        return
    if not os.path.exists(args.transactions):
        print(f'Error: transactions file not found: {args.transactions}')
        return
    df_out, df_res = run_pipeline(args.disputes, args.transactions, args.out_classified, args.out_resolutions)
    print('Pipeline complete. Outputs written:')
    print(' -', args.out_classified)
    print(' -', args.out_resolutions)

if __name__ == '__main__':
    main()
