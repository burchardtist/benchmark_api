import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-compare-result',
  templateUrl: './compare-result.component.html',
  styleUrls: ['./compare-result.component.css'],
 
})
export class CompareResultComponent implements OnInit {


  @Input() title;
  @Input() data;


  showXAxis = true;
  showYAxis = true;
  gradient = false;
  showLegend = false;
  showXAxisLabel = true;
  xAxisLabel = 'Kwartyl';
  showYAxisLabel = true;
  yAxisLabel = 'Wynik';

  colorScheme = 'vivid';
  view: any[] = [600, 400];

  constructor() { }

  ngOnInit() {
  }

}
