import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {HotDogResultComponent} from './hot-dog-result.component';

describe('HotDogResultComponent', () => {
  let component: HotDogResultComponent;
  let fixture: ComponentFixture<HotDogResultComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HotDogResultComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HotDogResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
