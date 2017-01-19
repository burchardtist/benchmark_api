import { DatabaseBenchmarkPage } from './app.po';

describe('database-benchmark App', function() {
  let page: DatabaseBenchmarkPage;

  beforeEach(() => {
    page = new DatabaseBenchmarkPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
