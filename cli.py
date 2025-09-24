import argparse
from .pipeline import run_pipeline
import logging
from .logging_setup import setup_logging

def main():
    parser = argparse.ArgumentParser(description='AI Dispute Assistant v2 CLI')
    parser.add_argument('--disputes', required=True, help='Path to disputes CSV')
    parser.add_argument('--transactions', required=True, help='Path to transactions CSV')
    parser.add_argument('--out_dir', default='/mnt/data', help='Output directory')
    args = parser.parse_args()
    setup_logging()
    logging.info('Starting pipeline with disputes=%s transactions=%s', args.disputes, args.transactions)
    run_pipeline(args.disputes, args.transactions, out_dir=args.out_dir)

if __name__ == '__main__':
    main()
