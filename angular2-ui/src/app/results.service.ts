import { Injectable } from '@angular/core';
import { BenchmarkInfo, BenchmarkResult, BenchmarkScore, Result, Serie } from './shared/models'
@Injectable()
export class ResultsService {

  constructor() { }

  convertToCurrentData(score: BenchmarkScore, name: string): Result {
    let result: Result = {
      name: name,
      series: [
        {
          name: "Insert",
          value: score.insert_time
        },
        {
          name: "Select",
          value: score.select_time
        },
        {
          name: "Select Indexed",
          value: score.select_index_time
        },
        {
          name: "Update",
          value: score.update_time
        },
        {
          name: "Update Indexed",
          value: score.update_index_time
        }
      ]
    }
    return result;
  }

  convertToCompareData(result: BenchmarkResult): Result[] {
    let scores: { title: string, score: BenchmarkScore }[] = [];
    scores.push({
      title: "Najlepszy wynik",
      score: result.bestTotalTime,
    });
    scores.push({
      title: "Najgorszy wynik",
      score: result.worstTotalTime,
    });
    scores.push({
      title: "Twój wynik",
      score: result.benchmarkResult,
    });
    result.systemOtherResults.forEach((score, i) => {
      scores.push({
        title: `${i+1}. kwartyl`,
        score: score,
      });
    })
    scores = scores.sort((a, b) => { return b.score.score - a.score.score });

    let results: Result[] = [];
    scores.forEach((score) => {
      results.push(this.convertToCurrentData(score.score, score.title));
    })
    return results;
  }

  convertToRankingData(result: BenchmarkResult): Serie[] {
    let serie: Serie[] = [
      {
        name: "Najlepszy wynik",
        value: result.bestTotalTime.score,
        id: result.bestTotalTime.id
      },
      {
        name: "Twój wynik",
        value: result.benchmarkResult.score,
        id: result.benchmarkResult.id
        
      },
      {
        name: "Najgorszy wynik",
        value: result.worstTotalTime.score,
        id: result.worstTotalTime.id
        
      },
    ]
    return serie;
  }

}
