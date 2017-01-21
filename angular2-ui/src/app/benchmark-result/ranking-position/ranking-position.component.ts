import { Component, EventEmitter, Output, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-ranking-position',
  templateUrl: './ranking-position.component.html',
  styleUrls: ['./ranking-position.component.css']
})
export class RankingPositionComponent implements OnInit {

  @Input()
  data
  @Input()
  count: number;
  @Input()
  ranking: number;
  view: any[] = [550, 150];

  colorScheme = 'nightLights';



  constructor() {

    
  }



  ngOnInit() {
  }

}
