import { Component, onWillStart, useEffect, useRef, useState } from "@odoo/owl";
import { loadBundle } from "@web/core/assets";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";

export class Tablero extends Component {
    static template = "donofrio_tablero.Tablero";
    static props = { ...standardActionServiceProps };

    setup() {
        this.orm = useService("orm");
        this.graficoRef = useRef("grafico");
        this.grafico = null;
        this.state = useState({ kpis: null, almacenId: false });

        onWillStart(async () => {
            await loadBundle("web.chartjs_lib");
            await this.cargar();
        });
        useEffect(
            () => {
                this.dibujarGrafico();
                return () => this.destruirGrafico();
            },
            () => [this.state.kpis]
        );
    }

    async cargar() {
        this.state.kpis = await this.orm.call("donofrio.tablero", "get_kpis", [], {
            warehouse_id: this.state.almacenId,
        });
    }

    async onCambiarAlmacen(ev) {
        this.state.almacenId = ev.target.value ? parseInt(ev.target.value, 10) : false;
        await this.cargar();
    }

    formatoNumero(valor, decimales = 0) {
        return new Intl.NumberFormat("es-PE", {
            minimumFractionDigits: decimales,
            maximumFractionDigits: decimales,
        }).format(valor);
    }

    formatoDinero(valor) {
        const { moneda, decimales } = this.state.kpis;
        return `${moneda} ${this.formatoNumero(valor, decimales)}`;
    }

    formatoPorcentaje(valor) {
        return valor === null ? "Sin datos" : `${this.formatoNumero(valor, 1)} %`;
    }

    /** Las tarjetas del tablero; las de módulos no instalados no vienen de `get_kpis`. */
    get tarjetas() {
        const k = this.state.kpis;
        const tarjetas = [];
        const ventas = k.ventas_mes;
        let comparacion = "Sin ventas el mes anterior";
        if (ventas.variacion_pct !== null) {
            const signo = ventas.variacion_pct > 0 ? "+" : "";
            comparacion = `${signo}${this.formatoNumero(ventas.variacion_pct, 1)} % vs. mes anterior`;
        }
        tarjetas.push({
            clave: "ventas_mes",
            titulo: "Ventas del mes",
            valor: this.formatoDinero(ventas.total),
            detalle: comparacion,
        });
        tarjetas.push({
            clave: "produccion",
            titulo: "Cumplimiento de producción",
            valor: this.formatoPorcentaje(k.produccion.cumplimiento_pct),
            detalle: `${k.produccion.hechas} de ${k.produccion.planificadas} OP del mes`,
        });
        tarjetas.push({
            clave: "stock_por_vencer",
            titulo: `Stock por vencer (${k.stock_por_vencer.dias} d)`,
            valor: `${k.stock_por_vencer.lotes} lotes`,
            detalle: `Valor ${this.formatoDinero(k.stock_por_vencer.valor)} · ${k.stock_por_vencer.vencidos} vencidos`,
        });
        if (k.lotes_aprobados) {
            tarjetas.push({
                clave: "lotes_aprobados",
                titulo: "Lotes aprobados",
                valor: this.formatoPorcentaje(k.lotes_aprobados.aprobados_pct),
                detalle: `${k.lotes_aprobados.aprobados} de ${k.lotes_aprobados.inspeccionados} inspeccionados`,
            });
        }
        if (k.liquidaciones_pendientes) {
            tarjetas.push({
                clave: "liquidaciones_pendientes",
                titulo: "Liquidaciones pendientes",
                valor: `${k.liquidaciones_pendientes.cantidad}`,
                detalle: "Heladeros sin liquidar",
            });
        }
        if (k.alertas_temperatura) {
            tarjetas.push({
                clave: "alertas_temperatura",
                titulo: "Alertas de temperatura",
                valor: `${k.alertas_temperatura.cantidad}`,
                detalle: `Fuera de rango en los últimos ${k.alertas_temperatura.dias} días`,
            });
        }
        return tarjetas;
    }

    destruirGrafico() {
        if (this.grafico) {
            this.grafico.destroy();
            this.grafico = null;
        }
    }

    dibujarGrafico() {
        if (!this.graficoRef.el || !this.state.kpis) {
            return;
        }
        this.destruirGrafico();
        const meses = this.state.kpis.ventas_por_mes;
        this.grafico = new Chart(this.graficoRef.el, {
            type: "bar",
            data: {
                labels: meses.map((m) => m.etiqueta),
                datasets: [
                    {
                        label: "Ventas",
                        data: meses.map((m) => m.total),
                        backgroundColor: "#F7C60A",
                        borderColor: "#9A6B00",
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } },
            },
        });
    }
}

registry.category("actions").add("donofrio_tablero.tablero", Tablero);
