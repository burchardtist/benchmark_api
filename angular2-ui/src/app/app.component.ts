import { Component } from '@angular/core';
import { BenchmarkService } from './benchmark.service';
import { MdDialog } from '@angular/material';
import { FailDialogComponent } from './fail-dialog/fail-dialog.component';
import { RegisterResult } from './shared/models/register-result.model';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  benchmarkIdValue: number;
  set benchmarkId(id) {
    this.benchmarkIdValue = id;
    let link = this.tabLinks.find(l => l.label === 'Twój wynik');
    if (id) {
      link.visible = true;
      link.link = `Result/${id}`;
    } else {
      link.visible = false;
    }
  }

  get benchmarkId() {
    return this.benchmarkIdValue;
  }


  tabLinks = [
    { label: 'Wyniki', link: 'List', visible: true },
    { label: 'Wykonaj test', link: 'NewBenchmark', visible: true },
    { label: 'Twój wynik', link: 'Result/26', visible: false },
  ];
  activeLinkIndex = 0;

  constructor(private benchmarkService: BenchmarkService, private dialog: MdDialog) {
  }

  ngOnInit() {
    this.benchmarkService.benchmarkId$.subscribe((id) => {
      this.benchmarkId = id;
    })
  }



}

