import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartTypeSelectComponent } from './chart-type-select.component';

describe('ChartTypeSelectComponent', () => {
  let component: ChartTypeSelectComponent;
  let fixture: ComponentFixture<ChartTypeSelectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChartTypeSelectComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChartTypeSelectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
