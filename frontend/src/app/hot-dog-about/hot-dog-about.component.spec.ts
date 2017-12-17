import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {HotDogAboutComponent} from './hot-dog-about.component';

describe('HotDogAboutComponent', () => {
  let component: HotDogAboutComponent;
  let fixture: ComponentFixture<HotDogAboutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HotDogAboutComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HotDogAboutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
