import { Injectable } from '@angular/core';
import { Http, URLSearchParams } from '@angular/http';
import { Router } from '@angular/router';


import { BenchmarkData } from './benchmark-form/bechmark-data.model';
import { TestStatus } from './shared/models/test-status.model';
import { BenchmarkResult } from './shared/models/benchmark-result.model';
import { BenchmarkInfo } from './shared/models/benchmark-info.model';
import { DatabaseSystem } from './shared/constants/database-system.enum';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/interval';

import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/startWith';


import { Subject } from 'rxjs/Subject';



@Injectable()
export class BenchmarkService {

  benchmarkId: number;
  benchmarkId$: Observable<number>;
  benchmarkIdSource: Subject<number>;

  constructor(private http: Http, private router: Router) {
    this.benchmarkIdSource = new Subject();
    this.benchmarkId$ = this.benchmarkIdSource.asObservable();
  }

  setBenchmarkId(id: number) {
    this.benchmarkId = id;
    this.benchmarkIdSource.next(id);
  }

  showResult(id: number) {
      this.router.navigate([`Result/${id}`])
  }

  startPolling(id: number, interval: number) {
    return Observable.interval(interval).startWith(0)
      .switchMap(() => this.getTestStatus(id));
  }


  registerBenchmark(data: BenchmarkData): Observable<TestStatus> {
    let body = new URLSearchParams();
    body.set('systemId', String(data.systemId));
    body.set('address', data.address);
    body.set('port', String(data.port));
    body.set('user', data.user);
    body.set('password', data.password);
    body.set('database', data.database);

    return this.http.post('/api/RegisterBenchmark',
      body
    ).map((data) => data.json())
  }


  getTestStatus(id: number): Observable<TestStatus> {
    return this.http.get(`/api/GetTest?benchmarkId=${id}`).map((data) => data.json())
  }

  getTestResult(id: number): Observable<BenchmarkResult> {
    return this.http.get(`/api/BenchmarkResult?benchmarkId=${id}`).map((data) => data.json())
  }

  getBenchmarkList(databaseSystem: DatabaseSystem): Observable<BenchmarkInfo[]> {
    return this.http.get(`/api/GetList?systemId=${databaseSystem}`).map((data) => data.json().result)
  }



}
