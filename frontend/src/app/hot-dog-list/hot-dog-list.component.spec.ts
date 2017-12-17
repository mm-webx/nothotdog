import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {HotDogListComponent} from './hot-dog-list.component';

describe('HotDogListComponent', () => {
  let component: HotDogListComponent;
  let fixture: ComponentFixture<HotDogListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [HotDogListComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(HotDogListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
