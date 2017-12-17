import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {HotDogDetailsComponent} from './hot-dog-details.component';

describe('HotDogDetailsComponent', () => {
  let component: HotDogDetailsComponent;
  let fixture: ComponentFixture<HotDogDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HotDogDetailsComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HotDogDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
