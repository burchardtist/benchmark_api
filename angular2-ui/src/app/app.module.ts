import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { MaterialModule } from '@angular/material';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { DataTableModule, SharedModule } from 'primeng/primeng';

import { AppComponent } from './app.component';
import { BenchmarkFormComponent } from './benchmark-form/benchmark-form.component';
import { BenchmarkService } from './benchmark.service';
import { ResultsService } from './results.service';

import { FailDialogComponent } from './fail-dialog/fail-dialog.component';
import { BenchmarkResultComponent } from './benchmark-result/benchmark-result.component';
import { CurrentResultComponent } from './benchmark-result/current-result/current-result.component';
import { RankingPositionComponent } from './benchmark-result/ranking-position/ranking-position.component';
import { CompareResultComponent } from './benchmark-result/compare-result/compare-result.component';
import { BenchmarkListComponent } from './benchmark-list/benchmark-list.component';
import { AppRoutingModule } from './app-routing.module';
import { BenchmarkActualComponent } from './benchmark-actual/benchmark-actual.component';


@NgModule({
  declarations: [
    AppComponent,
    BenchmarkFormComponent,
    FailDialogComponent,
    BenchmarkResultComponent,
    CurrentResultComponent,
    RankingPositionComponent,
    CompareResultComponent,
    BenchmarkListComponent,
    BenchmarkActualComponent
  ],
  entryComponents: [FailDialogComponent],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    MaterialModule.forRoot(),
    NgxChartsModule,
    DataTableModule,
    SharedModule,
    AppRoutingModule
  ],
  providers: [BenchmarkService, ResultsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
