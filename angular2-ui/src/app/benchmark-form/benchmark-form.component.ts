import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { BenchmarkData } from './bechmark-data.model';
import { DatabaseSystems } from '../shared/constants/database-system.enum';
@Component({
  selector: 'app-benchmark-form',
  templateUrl: './benchmark-form.component.html',
  styleUrls: ['./benchmark-form.component.css']
})
export class BenchmarkFormComponent implements OnInit {
  databaseSystems = DatabaseSystems;

  @Output()
  save: EventEmitter<BenchmarkData> = new EventEmitter<BenchmarkData>();

  data: BenchmarkData = new BenchmarkData();
  onSubmit() {
    this.save.emit(this.data);
  }

  constructor() { }

  ngOnInit() {
  }

}
