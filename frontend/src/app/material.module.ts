import {MatButtonModule, MatSidenavModule, MatToolbarModule} from '@angular/material';
import {NgModule} from "@angular/core";

@NgModule({
  imports: [
    MatButtonModule,
    MatSidenavModule,
    MatToolbarModule
  ],
  exports: [
    MatButtonModule,
    MatSidenavModule,
    MatToolbarModule
  ],
})
export class MaterialModule {
}
