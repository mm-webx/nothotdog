import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {HotDogHomeComponent} from './hot-dog-home.component';

describe('HotDogHomeComponent', () => {
  let component: HotDogHomeComponent;
  let fixture: ComponentFixture<HotDogHomeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HotDogHomeComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HotDogHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
