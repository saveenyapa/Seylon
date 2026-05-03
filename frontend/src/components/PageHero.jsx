export default function PageHero({ eyebrow, title, lead, bgImage }) {
  return (
    <section className="page-hero">
      <div
        className="page-hero-bg"
        style={{ backgroundImage: `url('${bgImage}')` }}
      />
      <div className="hero-content container">
        <div className="eyebrow left">{eyebrow}</div>
        <h1 dangerouslySetInnerHTML={{ __html: title }} />
        {lead && <p className="lead">{lead}</p>}
      </div>
    </section>
  )
}
