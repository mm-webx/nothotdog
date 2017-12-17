import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {HotDogAddComponent} from './hot-dog-add.component';

describe('HotDogAddComponent', () => {
  let component: HotDogAddComponent;
  let fixture: ComponentFixture<HotDogAddComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HotDogAddComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HotDogAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
