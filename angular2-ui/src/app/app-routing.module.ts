import { NgModule }              from '@angular/core';
import { RouterModule, Routes }  from '@angular/router';
import { BenchmarkActualComponent }   from './benchmark-actual/benchmark-actual.component';
import { BenchmarkResultComponent } from './benchmark-result/benchmark-result.component';
import { BenchmarkListComponent } from './benchmark-list/benchmark-list.component';
BenchmarkActualComponent


const appRoutes: Routes = [
  { path: '', redirectTo: 'List' ,  pathMatch: 'full'},
  { path: 'List',        component: BenchmarkListComponent },
  { path: 'NewBenchmark',        component: BenchmarkActualComponent },
  { path: 'Result/:id',        component: BenchmarkResultComponent }
  
  
];
@NgModule({
  imports: [
    RouterModule.forRoot(appRoutes,{  useHash: true})
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule {}