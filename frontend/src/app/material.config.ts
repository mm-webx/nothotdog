import {MatButtonModule, MatIconModule, MatSidenavModule, MatToolbarModule} from '@angular/material';
import {NgModule} from "@angular/core";

@NgModule({
  imports: [
    MatButtonModule,
    MatSidenavModule,
    MatToolbarModule,
    MatIconModule
  ],
  exports: [
    MatButtonModule,
    MatSidenavModule,
    MatToolbarModule,
    MatIconModule
  ],
})
export class MaterialModule {
}
