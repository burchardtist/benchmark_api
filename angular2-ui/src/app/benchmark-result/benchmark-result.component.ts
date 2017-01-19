import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { BenchmarkService } from '../benchmark.service'
import { ResultsService } from '../results.service'


@Component({
  selector: 'app-benchmark-result',
  templateUrl: './benchmark-result.component.html',
  styleUrls: ['./benchmark-result.component.css']
})
export class BenchmarkResultComponent implements OnInit {

  compareData;
  rankingData;
  currentData;
  ranking: number;
  count: number;
  loaded: boolean;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private benchmarkService: BenchmarkService,
    private resultsService: ResultsService
  ) { }

  ngOnInit() {
    let id = +this.route.snapshot.params['id'];
    this.benchmarkService.getTestResult(id).subscribe((data) => {
      this.compareData = this.resultsService.convertToCompareData(data);
      this.rankingData = this.resultsService.convertToRankingData(data);
      this.currentData = this.resultsService.convertToCurrentData(data.benchmarkResult, "Wynik");
      this.ranking = data.rankingPosition + 1;
      this.count = data.totalBenchmarksCount;
      this.loaded = true;
    })
  }

}
