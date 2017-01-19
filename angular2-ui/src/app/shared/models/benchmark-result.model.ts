import { BenchmarkScore } from './benchmark-score.model';

export class BenchmarkResult {
    benchmarkId: number;
    rankingPosition: number;
    totalBenchmarksCount: number;
    bestTotalTime: BenchmarkScore;
    worstTotalTime: BenchmarkScore;
    benchmarkResult: BenchmarkScore;
    systemOtherResults: BenchmarkScore[];
}

