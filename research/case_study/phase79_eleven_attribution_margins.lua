-- Typeset the generator's audit signs in the margin. Full notes are in the ledger.
function Div(el)
  if el.classes:includes('audit-margin') then
    if FORMAT:match('latex') then
      local codes = el.attributes['data-codes'] or ''
      local identifier = el.attributes['data-note'] or ''
      if not codes:match('^[BIRCVLMO ]+$') or not identifier:match('^[A-Z0-9]+$') then
        error('invalid audit margin identifier')
      end
      local signs = {}
      for code in codes:gmatch('%u') do table.insert(signs, '[' .. code .. ']') end
      return pandoc.RawBlock('latex', '\\marginpar{\\raggedright\\scriptsize '
        .. table.concat(signs, ' ') .. '\\\\ ' .. identifier .. '}')
    end
    return el.content
  end
end
