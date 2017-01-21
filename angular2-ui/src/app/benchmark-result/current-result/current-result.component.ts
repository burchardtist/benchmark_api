import { Component, Input, OnInit } from '@angular/core';

import { Result } from '../../shared/models/results.model'
@Component({
  selector: 'app-current-result',
  templateUrl: './current-result.component.html',
  styleUrls: ['./current-result.component.css']
})
export class CurrentResultComponent implements OnInit {

 
  @Input()
  data: Result;

  view: any[] = [600, 400];
  colorScheme = "nightLights"

  // options
  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = false;
  showXAxisLabel = true;
  xAxisLabel = 'Typ operacji';
  showYAxisLabel = true;
  yAxisLabel = 'Czas [ms]';
  constructor() { }

  ngOnInit() {
  }

}
