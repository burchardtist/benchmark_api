import { Component, OnInit } from '@angular/core';


import { DatabaseSystems, DatabaseSystem } from '../shared/constants/database-system.enum';
import { BenchmarkInfo } from '../shared/models/benchmark-info.model';
import { BenchmarkService } from '../benchmark.service';



@Component({
  selector: 'app-benchmark-list',
  templateUrl: './benchmark-list.component.html',
  styleUrls: ['./benchmark-list.component.css']
})
export class BenchmarkListComponent implements OnInit {

  databaseSystems = DatabaseSystems;
  selectedSystem: DatabaseSystem = 1;
  scoreList: BenchmarkInfo[] = [];

  constructor(private benchmarkService: BenchmarkService) { }

  ngOnInit() {
    this.loadData();
  }

  selectSystem(system: DatabaseSystem) {
      this.loadData();
  }
  selectResult(selected) {
         this.benchmarkService.showResult(selected.id); 

  }

  loadData() {
    this.benchmarkService.getBenchmarkList(this.selectedSystem).subscribe((data) => {
      this.scoreList = data;
    }
    )
  }

}
