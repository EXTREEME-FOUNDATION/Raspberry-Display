const Applet = imports.ui.applet;
const Util = imports.misc.util;

function MyApplet(orientation, panel_height, instance_id) {
    this._init(orientation, panel_height, instance_id);
}

MyApplet.prototype = {
    __proto__: Applet.IconApplet.prototype,

    _init: function(orientation, panel_height, instance_id) {
        Applet.IconApplet.prototype._init.call(this, orientation, panel_height, instance_id);

        this.set_applet_icon_name("EX-raspi-connect");
        this.set_applet_tooltip(_("Control the raspi display via the mouse"));
    },

    on_applet_clicked: function() {
        Util.spawn('xed');
    }
};

function main(metadata, orientation, panel_height, instance_id) {
    return new MyApplet(orientation, panel_height, instance_id);
}
