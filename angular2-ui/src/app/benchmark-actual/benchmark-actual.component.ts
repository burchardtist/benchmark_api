import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Subscription } from 'rxjs/Subscription';

import { BenchmarkService } from '../benchmark.service';

@Component({
  selector: 'app-benchmark-actual',
  templateUrl: './benchmark-actual.component.html',
  styleUrls: ['./benchmark-actual.component.css']
})
export class BenchmarkActualComponent implements OnInit {

  TIME: number = 10000;
  benchmarkId: number;
  status: string;
  pollingSubscription: Subscription;
  constructor(private benchmarkService: BenchmarkService, private router: Router) { }

  onSave(data) {
    this.startBenchmark(data);

  }

  startBenchmark(data) {
    this.benchmarkService.registerBenchmark(data).subscribe((result) => {
      this.benchmarkId = result.benchmark_id;
      this.status = result.status;
      this.startPolling(this.benchmarkId);
    });
  }

  startPolling(id: number) {
    this.pollingSubscription = this.benchmarkService.startPolling(id, this.TIME).subscribe((data) => {
      this.status = data.status;

      if (data.status === 'fail') {
        this.pollingSubscription.unsubscribe();
      }
      if (data.status === 'done') {
      this.benchmarkService.setBenchmarkId(this.benchmarkId);
        
        this.pollingSubscription.unsubscribe();

        this.router.navigate([`Result/${id}`])
      }

    })
  }


  ngOnInit() {
  }

}
